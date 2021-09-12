/* Automatically generated nanopb constant definitions */
/* Generated by nanopb-0.4.5 */

#include "gtfs-realtime.pb.h"
#if PB_PROTO_HEADER_VERSION != 40
#error Regenerate this file with the current version of nanopb generator.
#endif

PB_BIND(transit_realtime_FeedMessage, transit_realtime_FeedMessage, 2)


PB_BIND(transit_realtime_FeedHeader, transit_realtime_FeedHeader, 2)


PB_BIND(transit_realtime_FeedEntity, transit_realtime_FeedEntity, 2)


PB_BIND(transit_realtime_TripUpdate, transit_realtime_TripUpdate, 2)


PB_BIND(transit_realtime_TripUpdate_StopTimeEvent, transit_realtime_TripUpdate_StopTimeEvent, 2)


PB_BIND(transit_realtime_TripUpdate_StopTimeUpdate, transit_realtime_TripUpdate_StopTimeUpdate, 2)


PB_BIND(transit_realtime_VehiclePosition, transit_realtime_VehiclePosition, 2)


PB_BIND(transit_realtime_Alert, transit_realtime_Alert, 2)


PB_BIND(transit_realtime_TimeRange, transit_realtime_TimeRange, 2)


PB_BIND(transit_realtime_Position, transit_realtime_Position, 2)


PB_BIND(transit_realtime_TripDescriptor, transit_realtime_TripDescriptor, 2)


PB_BIND(transit_realtime_VehicleDescriptor, transit_realtime_VehicleDescriptor, 2)


PB_BIND(transit_realtime_EntitySelector, transit_realtime_EntitySelector, 2)


PB_BIND(transit_realtime_TranslatedString, transit_realtime_TranslatedString, 2)


PB_BIND(transit_realtime_TranslatedString_Translation, transit_realtime_TranslatedString_Translation, 2)











#ifndef PB_CONVERT_DOUBLE_FLOAT
/* On some platforms (such as AVR), double is really float.
 * To be able to encode/decode double on these platforms, you need.
 * to define PB_CONVERT_DOUBLE_FLOAT in pb.h or compiler command line.
 */
PB_STATIC_ASSERT(sizeof(double) == 8, DOUBLE_MUST_BE_8_BYTES)
#endif

