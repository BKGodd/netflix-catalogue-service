import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators'

interface AggObject {
  total: Observable<any>
  movie: Observable<any>
  show: Observable<any>
}

@Injectable({
  providedIn: 'root'
})
export class AggsService {
  private aggData$: Observable<any>;
  private aggMovieData$: Observable<any>;
  private aggShowData$: Observable<any>;

  private dataTotal = {'director_agg': {'Rajiv Chilaka': 19,
                              'Raúl Campos, Jan Suter': 18,
                              'Marcus Raboy': 16,
                              'Suhas Kadav': 16,
                              'Jay Karas': 14},
                            'actor_agg': {'Anupam Kher': 43,
                              'Shah Rukh Khan': 35,
                              'Julie Tejwani': 33,
                              'Naseeruddin Shah': 32,
                              'Takahiro Sakurai': 32},
                            'rating_agg': {'TV-MA': 3207,
                              'TV-14': 2160,
                              'TV-PG': 863,
                              'R': 799,
                              'PG-13': 490},
                            'country_agg': {'United States': 2818,
                              'India': 972,
                              'United Kingdom': 419,
                              'Japan': 245,
                              'South Korea': 199},
                            'genre_agg': {'International Movies': 2752,
                              'Dramas': 2427,
                              'Comedies': 1674,
                              'International TV Shows': 1351,
                              'Documentaries': 869},
                            'total_agg': 8807};
    private dataMovie = {'histo_dur_agg': {'0': 25,
        '20': 144,
        '40': 288,
        '60': 592,
        '80': 2156,
        '100': 1724,
        '120': 770,
        '140': 271,
        '160': 108,
        '180': 29,
        '200': 11,
        '220': 6,
        '240': 1,
        '260': 1,
        '280': 0,
        '300': 1},
       'avg_dur_agg': 99,
       'total_agg': 6131}
    private dataShow = {'total_agg': 2676}

  constructor(private http: HttpClient) {
    this.aggData$ = this.http.get<any>('/api/aggs/').pipe(
      map((data) => this.cleanData(data)),
      shareReplay(1));
    this.aggMovieData$ = this.http.get<any>('/api/aggs/movie/').pipe(
      map((data) => this.cleanData(data)),
      shareReplay(1));
    this.aggShowData$ = this.http.get<any>('/api/aggs/show/').pipe(
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
}
