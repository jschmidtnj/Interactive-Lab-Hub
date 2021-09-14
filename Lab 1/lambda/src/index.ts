import { APIGatewayProxyEventV2, APIGatewayProxyHandlerV2 } from 'aws-lambda';
import { APIPassword, ferryAPI, ferryStopID, FSubwayStopID, initializeConfig, mtaAPIKey, timezone, subwayAPI } from './config';
import { initializeLogger } from './logger';
import axios from 'axios';
import GTFSRealtimeBindings from 'gtfs-realtime-bindings-transit';
import HTTPStatus from 'http-status-codes';
import { utcToZonedTime, zonedTimeToUtc } from 'date-fns-tz';
import { addMinutes, format, roundToNearestMinutes } from 'date-fns';

const convertToTimezone = (dates: Date[]) => dates.map(date => utcToZonedTime(date, timezone));

const getSubwayData = async (limit: number | undefined = undefined, useTimezone = false): Promise<Date[]> => {
  const subwayRes = await axios.get(subwayAPI, {
    headers: {
      'x-api-key': mtaAPIKey
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
      if (update.stopId !== FSubwayStopID || !update.arrival) {
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

const getFerryData = async (limit: number | undefined = undefined, useTimezone = false): Promise<Date[]> => {
  const ferryRes = await axios.get(ferryAPI, {
    responseType: 'arraybuffer'
  });
  if (ferryRes.status !== HTTPStatus.OK) {
    throw new Error('invalid status code for ferry data');
  }
  const data = GTFSRealtimeBindings.transit_realtime.FeedMessage.decode(ferryRes.data);

  let ferryTimes: Date[] = [];
  for (const entity of data.entity) {
    if (!entity.tripUpdate || !entity.tripUpdate.stopTimeUpdate) {
      continue;
    }
    for (const update of entity.tripUpdate.stopTimeUpdate) {
      if (update.stopId !== String(ferryStopID) || !update.arrival) {
        continue;
      }
      const timestamp = new Number(update.arrival.time);
      if (!timestamp) {
        continue;
      }
      ferryTimes.push(new Date(timestamp.valueOf() * 1000));
    }
  }
  if (limit !== undefined) {
    ferryTimes.splice(limit);
  }
  if (useTimezone) {
    ferryTimes = convertToTimezone(ferryTimes);
  }

  return ferryTimes;
};

const getTramData = (numTimes = 5, useTimezone = false): Date[] => {
  const minutesBetweenStops = 15;
  const endHour = 2;
  const startHour = 6;

  let currentTime = utcToZonedTime(new Date(), timezone);
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
    tramTimes.push(zonedTimeToUtc(currentTime, timezone));
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
  if (token !== APIPassword) {
    throw new Error('unauthorized');
  }
};

export const handler: APIGatewayProxyHandlerV2 = async (event) => {
  try {
    initializeConfig();
    initializeLogger();
    authorize(event);
    const limit = 5;
    const subwayData = await getSubwayData(limit);
    const ferryData = await getFerryData(limit);
    const tramData = getTramData(limit);
    return {
      statusCode: HTTPStatus.OK,
      body: JSON.stringify({
        subway: subwayData,
        ferry: ferryData,
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
  initializeConfig();
  initializeLogger();
  const dateFormat = 'yyyy-MM-dd HH:mm';
  console.log(getTramData(5, true).map(date => format(date, dateFormat)));
  console.log(format(utcToZonedTime(new Date(), timezone), dateFormat));
};

if (require.main === module) {
  runAction().then(() => {
    console.log('got transit data');
  }).catch((err: Error) => {
    console.error(err.message);
  });
}

export default runAction;
