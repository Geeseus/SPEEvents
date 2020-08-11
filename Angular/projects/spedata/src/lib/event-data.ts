import { EventType } from "./event-type.enum";
import { ParticipantData } from "./participant-data"
import { TeamData } from "./team-data"

export interface EventData {
    type: EventType;
    title: string;
    descr: string;
    tag: string;
    teams: TeamData[];
    participants: ParticipantData[];
    poststart: Date;
    postend: Date;
    votestart: Date;
    voteend: Date;
    lastupdate: Date;
    stage: number;
    winner: string;
}
