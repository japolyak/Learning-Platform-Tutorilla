import type { ScheduleEventDto } from '@/modules/core/services/api/api.models';
import type { ScheduleEventModel } from '@/modules/schedule/models';
import { parseDate, parseTimestamp, type TimestampOrNull } from '@quasar/quasar-ui-qcalendar';

export class ScheduleUtils {
	public static toTimestamp(date: number | string | Date): TimestampOrNull {
		if (date instanceof Date) return parseDate(date);
		else if (typeof date === 'number') return parseDate(new Date(date));

		return parseTimestamp(date);
	}

	public static eventMapper(event: ScheduleEventDto): ScheduleEventModel {
		const timestamp = ScheduleUtils.toTimestamp(event.date);

		return {
			id: event.id,
			title: `${event.subjectName} | ${event.personName}`,
			date: timestamp.date,
			time: timestamp.time,
			duration: event.duration,
			type: event.type,
		}
	}
}
