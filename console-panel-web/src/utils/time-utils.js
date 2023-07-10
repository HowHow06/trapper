import moment from 'moment-timezone';

export class TimeUtils {
  static getDateFromUTCString(dateString) {
    return moment.utc(dateString).toDate();
  }

  static changeTimezone(dateISOString, timezone) {
    return moment(dateISOString).parseZone().tz(timezone, true).toISOString(true);
  }

  static getDatetimeStringFromUTC(dateString, format = 'DD/MM/YYYY, HH:mm:ss', timezone) {
    const utcMoment = moment.utc(dateString);
    if (timezone) {
      return utcMoment.tz(timezone).format(format);
    }
    return utcMoment.local().format(format);
  }

  static getDurationFromNow(dateString, isDateStringUTC = true) {
    let durationFromNow = (isDateStringUTC ? moment.utc(dateString) : moment(dateString))
      .local()
      .startOf('seconds')
      .fromNow();
    durationFromNow = durationFromNow.replace('minutes', 'mins');
    durationFromNow = durationFromNow.replace('minute', 'min');
    return durationFromNow;
  }
}
