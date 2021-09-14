import { config } from 'dotenv';

export let debug = true;
export const subwayAPI = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm';
export let mtaAPIKey = '';
export let APIPassword = '';
export const FSubwayStopID = 'B06N';
export const ferryAPI = 'http://nycferry.connexionz.net/rtt/public/utility/gtfsrealtime.aspx/tripupdate';
export const ferryStopID = 25;
export const timezone = 'America/New_York';

export const initializeConfig = (): void => {
  config();
  if (process.env.DEBUG) {
    debug = process.env.DEBUG === 'true';
  }
  if (!process.env.MTA_API_KEY) {
    throw new Error('cannot find mta api key');
  }
  mtaAPIKey = process.env.MTA_API_KEY;
  if (!process.env.API_PASSWORD) {
    throw new Error('cannot find api password');
  }
  APIPassword = process.env.API_PASSWORD;
};
