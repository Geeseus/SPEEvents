import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { EventData, TeamData } from 'spedata';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';

@Component({
  selector: 'app-event-display',
  templateUrl: './event-display.component.html',
  styleUrls: ['./event-display.component.css']
})
export class EventDisplayComponent implements OnInit {

  @Input() event: EventData;

  public teamColumns: string[] = ['name', 'points', 'actions'];
  public teamDataSource: MatTableDataSource<TeamData>;
  @ViewChild(MatSort, {static: true}) public teamSort: MatSort;

  public time: Date;
  public postingPhase: boolean = false;
  public votingPhase: boolean = false;

  constructor() { }

  ngOnInit(): void {
    this.event.poststart = new Date(this.event.poststart);
    this.event.postend = new Date(this.event.postend);
    this.event.votestart = new Date(this.event.votestart);
    this.event.voteend = new Date(this.event.voteend);
    if (this.event.lastupdate != null)
      this.event.lastupdate = new Date(this.event.lastupdate);
    this.teamDataSource = new MatTableDataSource(this.event.teams);
    this.teamDataSource.sort = this.teamSort;
    this.time = new Date();
    this.postingPhase = this.event.poststart < this.time && this.time < this.event.postend;
    this.votingPhase = this.event.votestart < this.time && this.time < this.event.voteend;
    setInterval(() => {
      this.time = new Date();
      this.postingPhase = this.event.poststart < this.time && this.time < this.event.postend;
      this.votingPhase = this.event.votestart < this.time && this.time < this.event.voteend;
    }, 1000);
  }

}
