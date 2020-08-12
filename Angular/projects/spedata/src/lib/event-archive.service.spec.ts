import { TestBed } from '@angular/core/testing';

import { EventArchiveService } from './event-archive.service';

describe('EventArchiveService', () => {
  let service: EventArchiveService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(EventArchiveService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
