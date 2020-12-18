import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ActivationEnd, ParamMap, Router, RouterEvent } from '@angular/router';
import { PostData } from './post-data'

import { GalleryItem, ImageItem, VideoItem, YoutubeItem } from '@ngx-gallery/core';

import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { filter, map, skip } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  user: String;
  posts$: Observable<GalleryItem[]>;

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.router.events.subscribe(e => {
      if (e instanceof ActivationEnd) {
        console.log(e.snapshot.queryParams);
        this.user = e.snapshot.queryParams['u'];
        this.posts$ = this.http.get<PostData[]>('https://events.shitpostemblem.xyz/data/advent2020/' + this.user + '.json').pipe(
          map(res => res.map(p => new ImageItem({ src: p.url, thumb: p.url })))
        );
      }
   });
  }
}
