import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PostValueCalculatorComponent } from './post-value-calculator.component';

describe('PostValueCalculatorComponent', () => {
  let component: PostValueCalculatorComponent;
  let fixture: ComponentFixture<PostValueCalculatorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PostValueCalculatorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PostValueCalculatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
