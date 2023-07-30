import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators'


// Define our interfaces from the responses of the API
interface AggObject {
  total: Observable<AggData>
  movie: Observable<AggMovieData>
  show: Observable<AggShowData>
}
interface AggData {
  director_agg: object
  actor_agg: object
  rating_agg: object
  country_agg: object
  genre_agg: object
  total_agg: number
}
interface AggMovieData {
  histo_dur_agg: object
  avg_dur_agg: number
  total_agg: number
}
interface AggShowData {
  total_agg: number
}


@Injectable({
  providedIn: 'root'
})
export class AggsService {
  private aggData$: Observable<AggData>;
  private aggMovieData$: Observable<AggMovieData>;
  private aggShowData$: Observable<AggShowData>;

  constructor(private http: HttpClient) {
    this.aggData$ = this.http.get<AggData>('/api/aggs/').pipe(
      map((data) => this.cleanData(data)),
      shareReplay(1));
    this.aggMovieData$ = this.http.get<AggMovieData>('/api/aggs/movie/').pipe(
      map((data) => this.cleanData(data)),
      shareReplay(1));
    this.aggShowData$ = this.http.get<AggShowData>('/api/aggs/show/').pipe(
      map((data) => this.cleanData(data)),
      shareReplay(1));
  }


  getData(): AggObject {
    return {
      total: this.aggData$,
      movie: this.aggMovieData$,
      show: this.aggShowData$
    }
  }


  cleanData(data: object) {
    // Clean the data to be easily used for NGX charts
    const newObject: any = {};
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
}
