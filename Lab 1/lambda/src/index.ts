import { APIGatewayProxyEventV2, APIGatewayProxyHandlerV2 } from 'aws-lambda';
import * as config from './config';
import { initializeLogger } from './logger';
import axios from 'axios';
import GTFSRealtimeBindings from 'gtfs-realtime-bindings-transit';
import HTTPStatus from 'http-status-codes';
import { utcToZonedTime, zonedTimeToUtc } from 'date-fns-tz';
import { addMinutes, format, parse, roundToNearestMinutes } from 'date-fns';
import AdmZip from 'adm-zip';
import csv from 'csvtojson';

export const convertToTimezone = (dates: Date[]): Date[] => dates.map(date => utcToZonedTime(date, config.timezone));

const getSubwayData = async (limit: number | undefined = undefined, useTimezone = false): Promise<Date[]> => {
  const subwayRes = await axios.get(config.subwayRealtimeAPI, {
    headers: {
      'x-api-key': config.mtaAPIKey
    },
    responseType: 'arraybuffer'
  });
  if (subwayRes.status !== HTTPStatus.OK) {
    throw new Error('invalid status code for subway data');
  }
  const data = GTFSRealtimeBindings.transit_realtime.FeedMessage.decode(subwayRes.data);

  let subwayTimes: Date[] = [];
  for (const entity of data.entity) {
    if (!entity.tripUpdate || entity.tripUpdate.trip.routeId !== 'F' || !entity.tripUpdate.stopTimeUpdate) {
      continue;
    }
    for (const update of entity.tripUpdate.stopTimeUpdate) {
      if (update.stopId !== config.FSubwayStopID || !update.arrival) {
        continue;
      }
      const timestamp = new Number(update.arrival.time);
      if (!timestamp) {
        continue;
      }
      subwayTimes.push(new Date(timestamp.valueOf() * 1000));
    }
  }
  if (limit !== undefined) {
    subwayTimes.splice(limit);
  }
  if (useTimezone) {
    subwayTimes = convertToTimezone(subwayTimes);
  }

  return subwayTimes;
};

const getStaticFerryData = async (limit: number | undefined = undefined, useTimezone = false): Promise<{times: Date[], id: string}> => {
  const ferryRes = await axios.get(config.ferryStaticAPI, {
    responseType: 'arraybuffer'
  });
  if (ferryRes.status !== HTTPStatus.OK) {
    throw new Error('invalid status code for ferry static data');
  }

  const zip = new AdmZip(ferryRes.data);
  const entries = zip.getEntries();

  const stops = entries.find(entry => entry.name === 'stops.txt');
  if (!stops) {
    throw new Error('cannot find stops file');
  }
  const stopsData = await csv().fromString(stops.getData().toString());
  const stop = stopsData.find(stop => stop.stop_name === config.ferryStopName);
  if (!stop) {
    throw new Error('cannot find ferry stop');
  }
  const stopID: string = stop.stop_id;

  const stopTimes = entries.find(entry => entry.name === 'stop_times.txt');
  if (!stopTimes) {
    throw new Error('cannot find stop times file');
  }
  const stopTimesData = await csv().fromString(stopTimes.getData().toString());

  const givenFerryStops: Record<string, string>[] = stopTimesData.filter(stop => stop.stop_id === stopID);
  const ferryTimesStr = givenFerryStops.map(stop => stop.arrival_time);

  let currentTime = new Date();
  let ferryTimes: Date[] = [];
  for (const ferryTimeStr of ferryTimesStr) {
    currentTime = parse(ferryTimeStr, 'HH:mm:ss', currentTime);
    ferryTimes.push(currentTime);
  }

  if (limit !== undefined) {
    ferryTimes.splice(limit);
  }
  if (useTimezone) {
    ferryTimes = convertToTimezone(ferryTimes);
  }

  return {
    times: ferryTimes,
    id: stopID
  };
};

const getTramData = (numTimes = 5, useTimezone = false): Date[] => {
  const minutesBetweenStops = 15;
  const endHour = 2;
  const startHour = 6;

  let currentTime = utcToZonedTime(new Date(), config.timezone);
  currentTime = roundToNearestMinutes(currentTime, {
    nearestTo: minutesBetweenStops
  });
  let tramTimes: Date[] = [];
  for (; tramTimes.length < numTimes; currentTime = addMinutes(currentTime, minutesBetweenStops)) {
    if (currentTime.getHours() > endHour && currentTime.getHours() < startHour) {
      continue;
    }
    if (currentTime.getHours() === endHour && currentTime.getMinutes() !== 0) {
      continue;
    }
    tramTimes.push(zonedTimeToUtc(currentTime, config.timezone));
  }
  if (useTimezone) {
    tramTimes = convertToTimezone(tramTimes);
  }

  return tramTimes;
};

const authorize = (event: APIGatewayProxyEventV2): void => {
  const authorizationKey = 'authorization';
  if (!(authorizationKey in event.headers)) {
    throw new Error('cannot find authorization in headers');
  }
  const splitElem = event.headers[authorizationKey]!.split('Bearer ');
  if (splitElem.length !== 2) {
    throw new Error('invalid token formatting');
  }
  const token = splitElem[1];
  if (token !== config.APIPassword) {
    throw new Error('unauthorized');
  }
};

export const handler: APIGatewayProxyHandlerV2 = async (event) => {
  try {
    config.initializeConfig();
    initializeLogger();
    authorize(event);
    const limit = 5;
    const subwayData = await getSubwayData(limit);
    const { times } = await getStaticFerryData(limit);
    const tramData = getTramData(limit);
    return {
      statusCode: HTTPStatus.OK,
      body: JSON.stringify({
        subway: subwayData,
        ferry: times,
        tram: tramData
      })
    };
  } catch (err) {
    const errObj = err as Error;
    return {
      statusCode: HTTPStatus.INTERNAL_SERVER_ERROR,
      body: JSON.stringify({
        error: errObj.message
      })
    };
  }
};

const runAction = async (): Promise<void> => {
  config.initializeConfig();
  initializeLogger();
  const dateFormat = 'yyyy-MM-dd HH:mm:ss';
  console.log((await getStaticFerryData(5, true)).times.map(date => format(date, dateFormat)));
  console.log(format(utcToZonedTime(new Date(), config.timezone), dateFormat));
};

if (require.main === module) {
  runAction().then(() => {
    console.log('got transit data');
  }).catch((err: Error) => {
    console.error(err.message);
  });
}

export default runAction;
