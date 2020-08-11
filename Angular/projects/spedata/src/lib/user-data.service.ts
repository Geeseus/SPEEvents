import { Injectable } from '@angular/core';
import { Inject } from '@angular/core';
import { UserData } from './user-data';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'any'
})
export class UserDataService {
  constructor(
    @Inject('USER_DATA_URL') private dataUrl: string,
    private http: HttpClient) { }

    getUsers(): Observable<UserData[]> {
      return this.http.get<UserData[]>(this.dataUrl);
    }
}
