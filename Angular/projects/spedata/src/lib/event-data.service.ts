import { Injectable } from '@angular/core';
import { Inject } from '@angular/core';
import { EventData } from './event-data';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'any'
})
export class EventDataService {
  constructor(
    @Inject('EVENT_DATA_URL') private dataUrl: string,
    @Inject('EVENT_ARCHIVE_URL') private archiveUrl: string,
    private http: HttpClient) { }

  getEvents(): Observable<EventData[]> {
    return this.http.get<EventData[]>(this.dataUrl);
  }

  getArchived(): Observable<EventData[]> {
    return this.http.get<EventData[]>(this.archiveUrl);
  }
}
