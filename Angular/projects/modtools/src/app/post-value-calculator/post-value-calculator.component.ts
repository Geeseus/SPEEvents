import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-post-value-calculator',
  templateUrl: './post-value-calculator.component.html',
  styleUrls: ['./post-value-calculator.component.css']
})
export class PostValueCalculatorComponent implements OnInit {

  readonly pick_value = 1;
  readonly modification_value = 1;
  readonly text_character_value = 0.04;
  readonly combination_value = 1;
  readonly title_bonus_value = 1;
  readonly event_bonus_value = 2;
  readonly threshold = 10;

  public picks = 0;
  public modifications = 0;
  public combinations = 0;

  public text_chars = 0;
  public creation_total = 0;
  public modification_total = 0;

  public title_bonus = false;
  public event_bonus = false;

  public originality_factor = 1.0;

  constructor() { }

  ngOnInit(): void {
  }

  bonus_total(): number {
    var bonus = 0
    if (this.title_bonus)
      bonus += this.title_bonus_value;
    if (this.event_bonus)
      bonus += this.event_bonus_value;
    return bonus;
  }

  effort_value(): number {
    return this.picks * this.pick_value + this.modifications * this.modification_value + this.combinations * this.combination_value +
        this.text_chars * this.text_character_value + this.creation_total + this.modification_total + this.bonus_total();
  }

  post_value(): number {
    return this.effort_value() * this.originality_factor;
  }

}
