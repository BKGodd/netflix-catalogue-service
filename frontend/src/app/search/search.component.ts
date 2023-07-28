import { Component } from '@angular/core';
import { SearchService } from '../search.service';
import { setFadeInOut } from '../app.animation';


export interface SearchResult {
  title: string | null
  director: string | null
  cast: string[] | null
  country: string | null
  date_added: string | null
  release_year: number | null
  rating: string | null
  duration: number | null
  genres: string[] | null
  description: string | null
}

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css'],
  animations: [setFadeInOut]
})
export class SearchComponent {
  nullSearch = {title: "", director: "", cast: [], country: "",
                        date_added: "", release_year: -1, rating: "",
                        duration: -1, genres: [], description: ""};
  filmType = "movie";
  searchText = "";
  searchResult: SearchResult[] = [];
  validResults = true;
  errorRequest = false;
  anim_delays: number[] = Array.from({ length: 8 }, (_, index) => (index + 1) * 100);

  constructor(private searchService: SearchService) {}

  
  isCastArray(index: number): boolean {
    return Array.isArray(this.searchResult[index].cast) &&
      this.searchResult[index].cast!.length > 0;
  }
  isGenreArray(index: number): boolean {
    return Array.isArray(this.searchResult[index].genres) &&
      this.searchResult[index].genres!.length > 0;
  }

  onFilmTypeChange() {
    this.searchResult = [];
  }

  whileTyping() {
    this.searchResult = [];
  }

  enterKey(event: KeyboardEvent) {
    if (event.key == 'Enter' && this.searchText) {
      this.onSearch();
    }
  }

  onSearch() {
    this.searchService.getSearchData(this.filmType, this.searchText).subscribe(
      (result: SearchResult[]) => {
        this.searchResult = result;
        if (this.searchResult.length == 0) {
          this.validResults = false;
        } else {
          this.validResults = true;
          this.errorRequest = false;
          // Turn date_added into a human readable date
          for (let i = 0; i < this.searchResult.length; i++) {
            if (typeof this.searchResult[i].date_added == "string" ) {
              let date = this.searchResult[i].date_added!.slice(0, 2) + '/' + this.searchResult[i].date_added!.slice(2);
              date = date.slice(0, 5) + '/' + date.slice(5);
              this.searchResult[i].date_added = date;
            }
          }
        }
      },
      (error) => {
        this.searchResult = [];
        this.errorRequest = true;
        this.validResults = true;
        console.error('Error fetching data:', error);
      }
    )
  }
}
