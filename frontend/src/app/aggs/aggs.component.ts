import { Component, OnInit } from '@angular/core';
import { AggsService } from '../aggs.service';


@Component({
  selector: 'app-aggs',
  templateUrl: './aggs.component.html',
  styleUrls: ['./aggs.component.css'],
})
export class AggsComponent implements OnInit {
  aggResponse: any = {};
  aggMovieResponse: any = {};
  aggShowResponse: any = {};
  constructor(private aggsService: AggsService) { }

  ngOnInit() {
    // Subscribe to the aggs service observables for each type of aggregation
    for (const [aggType, aggObs] of Object.entries(this.aggsService.getData())) {
      aggObs.subscribe(
        (data: any) => {
          if (aggType === "total") {
            this.aggResponse = data;
          } else if (aggType === "movie") {
            this.aggMovieResponse = data;
          } else {
            this.aggShowResponse = data;
          }
        },
        (error: any) => {
          console.log(error)
        }
      )
    }
  }
}
