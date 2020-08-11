import { Component, OnInit } from '@angular/core';
import { EventData, EventType, TeamData } from 'dist/spedata';

@Component({
  selector: 'app-event-generator',
  templateUrl: './event-generator.component.html',
  styleUrls: ['./event-generator.component.css']
})
export class EventGeneratorComponent implements OnInit {

  public event: EventData = {
    type: EventType.WT,
    title: 'Title',
    descr: 'Description',
    tag: '[WT]',
    teams: [],
    participants: [],
    poststart: null,
    postend: null,
    votestart: null,
    voteend: null,
    lastupdate: null,
    stage: 0,
    winner: null
  }
  public time = new Date();
  public eventTypes = [];
  private teamStr = "";

  constructor() { }

  ngOnInit(): void {
    this.eventTypes = Object.values(EventType);

    setInterval(() => {
      this.time = new Date();
   }, 1000);
  }

  onEventTypeChanged (type: EventType): void {
    switch (type) {
      case EventType.WT:
        this.event.tag = "[WT]";
        this.event.teams = [];
        break;
      case EventType.Slapfight:
        this.event.tag = null;
        this.updateTeams(this.teamStr);
        break;
      case EventType.Contest:
        this.event.tag = "[Contest]";
        this.event.teams = [];
        break;
    }
  }

  onTeamsChanged (teams: string): void {
    this.teamStr = teams;
    this.updateTeams(teams);
  }

  private updateTeams (teams: string): void {
    if (teams.trim().length < 1) {
      this.event.teams = [];
      return;
    }
    this.event.teams = teams.split(',').map(team => {
      let result: TeamData = {
        name: team.trim(),
        points: 0
      };
      return result;
    });
  }

}
