import { trigger, transition, style, animate, AnimationTriggerMetadata } from '@angular/animations';


export const setFadeInOut: AnimationTriggerMetadata = trigger('setFadeInOut', [
    transition(':enter', [
      style({ opacity: 0 }),
      animate('800ms {{ duration }}ms', style({opacity: 1})),
    ]),
    transition(':leave', [animate('{{ duration }}ms', style({opacity: 0}))]),
  ]);
