import * as config from './config';
import axios from 'axios';
import GTFSRealtimeBindings from 'gtfs-realtime-bindings-transit';
import HTTPStatus from 'http-status-codes';

// does not have good data. might be useful in the future for something else
export const getRealtimeFerryData = async (ferryStopID: string, limit: number | undefined = undefined): Promise<Date[]> => {
  const ferryRes = await axios.get(config.ferryRealtimeAPI, {
    responseType: 'arraybuffer'
  });
  if (ferryRes.status !== HTTPStatus.OK) {
    throw new Error('invalid status code for ferry data');
  }
  const data = GTFSRealtimeBindings.transit_realtime.FeedMessage.decode(ferryRes.data);

  const ferryTimes: Date[] = [];
  for (const entity of data.entity) {
    console.log(entity.tripUpdate?.stopTimeUpdate?.map(elem => elem.stopId));
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

  return ferryTimes;
};
