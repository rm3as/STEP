#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

typedef struct{
    double x, y;
}City;

double distance(const City* city1, const City* city2){
    return sqrt(pow(city1->x - city2->x, 2) + pow(city1->y - city2->y, 2));
}

void nearest_neighbor_tsp(const City* cities, int num_cities, int*route){
    bool* visited = (bool*)malloc(num_cities + sizeof(bool));
    for (int i = 0; i < num_cities; ++i){
        visited[i] = false;
    }

    route[0] = 0;
    visited[0] = true;
    for (int i = 1; i < num_cities; ++i){
        int last = route[i-1];
        int next_city = -1;
        double min_dist = INFINITY;

        for (int j = 0; j < num_cities; ++j){
            if(!visited[j]){
                double dist = distance(&cities[last], &cities[j]);
                if(dist < min_dist){
                    min_dist = dist;
                    next_city = j;
                }
            }
        }
        route[i] = next_city;
        visited[next_city] = true;
    }

    route[num_cities] = 0; // Return to the start
    free(visited);
}

void two_opt(int* route, int num_cities, double** dist) {
    bool improved = true;

    while (improved) {
        improved = false;
        for (int i = 1; i < num_cities - 1; ++i) {
            for (int j = i + 1; j < num_cities; ++j) {
                if (j - i == 1) continue;
                int* new_route = (int*)malloc((num_cities + 1) * sizeof(int));
                for (int k = 0; k <= i - 1; ++k) {
                    new_route[k] = route[k];
                }
                for (int k = i; k <= j; ++k) {
                    new_route[k] = route[j - k + i];
                }
                for (int k = j + 1; k <= num_cities; ++k) {
                    new_route[k] = route[k];
                }

                double new_distance = 0.0;
                double best_distance = 0.0;

                for (int k = 0; k < num_cities; ++k) {
                    new_distance += dist[new_route[k]][new_route[k + 1]];
                    best_distance += dist[route[k]][route[k + 1]];
                }

                if (new_distance < best_distance) {
                    for (int k = 0; k <= num_cities; ++k) {
                        route[k] = new_route[k];
                    }
                    improved = true;
                }
                free(new_route);
            }
        }
    }
}

City* read_input(const char* filename, int* num_cities) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        perror("Error opening file");
        exit(EXIT_FAILURE);
    }

    // ヘッダー行を読み飛ばす
    char header[100];
    if (fgets(header, sizeof(header), file) == NULL) {
        perror("Failed to read header");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    int count = 0;
    double x, y;
    while (fscanf(file, "%lf,%lf", &x, &y) == 2) {
        count++;
    }
    // printf("count:%d", count);

    rewind(file);

    // ヘッダー行を読み飛ばす
    if (fgets(header, sizeof(header), file) == NULL) {
        perror("Failed to read header");
        fclose(file);
        exit(EXIT_FAILURE);
    }


    City* cities = (City*)malloc(count * sizeof(City));
    int i = 0;
    while (fscanf(file, "%lf,%lf", &x, &y) == 2) {
        cities[i].x = x;
        cities[i].y = y;
        i++;
    }

    fclose(file);

    *num_cities = count;
    return cities;
}

void print_tour(const int* tour, int num_cities) {
    for (int i = 0; i <= num_cities; ++i) {
        printf("%d\n", tour[i]);
    }
}




int* solve(const City* cities, int num_cities) {
    double** dist = (double**)malloc(num_cities * sizeof(double*));
    for (int i = 0; i < num_cities; ++i) {
        dist[i] = (double*)malloc(num_cities * sizeof(double));
        for (int j = 0; j < num_cities; ++j) {
            dist[i][j] = distance(&cities[i], &cities[j]);
        }
    }

    int* initial_route = (int*)malloc((num_cities + 1) * sizeof(int));
    nearest_neighbor_tsp(cities, num_cities, initial_route);

    two_opt(initial_route, num_cities, dist);

    for (int i = 0; i < num_cities; ++i) {
        free(dist[i]);
    }
    free(dist);

    return initial_route;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    int num_cities;
    City* cities = read_input(argv[1], &num_cities);
    for (int i = 0; i < num_cities; i++) {
        printf("City %d: x = %f, y = %f\n", i, cities[i].x, cities[i].y);
    }
    printf("num cities %d", num_cities);
    int* tour = solve(cities, num_cities);
    print_tour(tour, num_cities);

    free(cities);
    free(tour);

    return 0;
}
