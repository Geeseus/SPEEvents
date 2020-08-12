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

  constructor() { }

  ngOnInit(): void {
    this.teamDataSource = new MatTableDataSource(this.event.teams);
    this.teamDataSource.sort = this.teamSort;
  }

}
