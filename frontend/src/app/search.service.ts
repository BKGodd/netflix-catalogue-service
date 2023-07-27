import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class SearchService {
  constructor(private http: HttpClient) { }

  getSearchData(filmType: string, searchText: string): Observable<any> {
    return this.http.get<any>(`/api/film/${filmType}/`, {params: {"query": searchText}});
  }
}
