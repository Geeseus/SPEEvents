import { Component, OnInit } from '@angular/core';
import { EventData, EventDataService } from "dist/spedata";

@Component({
  selector: 'app-eventlist',
  templateUrl: './eventlist.component.html',
  styleUrls: ['./eventlist.component.css']
})
export class EventListComponent implements OnInit {

  public events: EventData[];

  constructor(private dataService: EventDataService) { }

  ngOnInit(): void {
    this.dataService.getEvents().subscribe((eventData: EventData[]) => this.events = eventData );
  }

}
