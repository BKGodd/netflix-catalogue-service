import { Component, OnInit } from '@angular/core';
import { AggsService } from '../aggs.service';
import { Observable } from 'rxjs';


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

  cleanData(data: Object) {
    var newObject: any = {};
    for (const [keyAgg, valueAgg] of Object.entries(data)) {
      if (typeof valueAgg === "object") {
        newObject[keyAgg] = [];
        for (const [key, value] of Object.entries(valueAgg)) {
          newObject[keyAgg].push({"name": key, "value": value})
        }
      } else {
        newObject[keyAgg] = valueAgg;
      }
    }

    return newObject;
  }


  ngOnInit() {
    this.aggsService.getData().subscribe(
      (data) => {
        console.log("FOUND")
        this.aggResponse = this.cleanData(data);
      },
      (error) => {
        console.log(error)
      }
    )
    /*
    this.aggsService.getData('/api/aggs/');
    this.aggsService.getData('/api/aggs/movie/');
    this.aggsService.getData('/api/aggs/show/');
    */
  }
}
