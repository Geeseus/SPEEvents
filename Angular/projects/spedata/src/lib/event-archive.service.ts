import { Injectable } from '@angular/core';
import { Inject } from '@angular/core';
import { EventData } from './event-data';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'any'
})
export class EventArchiveService {
  constructor(
    @Inject('EVENT_ARCHIVE_URL') private dataUrl: string,
    private http: HttpClient) { }

  getEvents(): Observable<EventData[]> {
    return this.http.get<EventData[]>(this.dataUrl);
  }
}
