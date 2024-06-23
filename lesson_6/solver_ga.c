#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <time.h>

#define POP_SIZE 100
#define MUTATION_RATE 0.1
#define GENERATIONS 500

typedef struct {
    double x, y;
} City;

typedef struct {
    int* tour;
    double fitness;
} Individual;

double distance(const City* city1, const City* city2) {
    return sqrt(pow(city1->x - city2->x, 2) + pow(city1->y - city2->y, 2));
}

void nearest_neighbor_tsp(const City* cities, int num_cities, int* route) {
    bool* visited = (bool*)malloc(num_cities * sizeof(bool));
    for (int i = 0; i < num_cities; ++i) {
        visited[i] = false;
    }

    route[0] = 0;
    visited[0] = true;
    for (int i = 1; i < num_cities; ++i) {
        int last = route[i - 1];
        int next_city = -1;
        double min_dist = INFINITY;

        for (int j = 0; j < num_cities; ++j) {
            if (!visited[j]) {
                double dist = distance(&cities[last], &cities[j]);
                if (dist < min_dist) {
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

double calculate_fitness(const int* tour, int num_cities, double** dist) {
    double total_distance = 0.0;
    for (int i = 0; i < num_cities; ++i) {
        total_distance += dist[tour[i]][tour[i + 1]];
    }
    return 1.0 / total_distance;
}

void mutate(int* tour, int num_cities) {
    if ((double)rand() / RAND_MAX < MUTATION_RATE) {
        int i = rand() % (num_cities - 1) + 1;
        int j = rand() % (num_cities - 1) + 1;
        int temp = tour[i];
        tour[i] = tour[j];
        tour[j] = temp;
    }
}

void crossover(const int* parent1, const int* parent2, int* child, int num_cities) {
    int start = rand() % num_cities;
    int end = rand() % num_cities;

    if (start > end) {
        int temp = start;
        start = end;
        end = temp;
    }

    bool* visited = (bool*)calloc(num_cities, sizeof(bool));
    for (int i = start; i <= end; ++i) {
        child[i] = parent1[i];
        visited[parent1[i]] = true;
    }

    int current_index = (end + 1) % num_cities;
    for (int i = 0; i < num_cities; ++i) {
        int city = parent2[(end + 1 + i) % num_cities];
        if (!visited[city]) {
            child[current_index] = city;
            current_index = (current_index + 1) % num_cities;
        }
    }
    free(visited);
}

void genetic_algorithm(const City* cities, int num_cities, int* best_tour, double** dist) {
    Individual population[POP_SIZE];
    for (int i = 0; i < POP_SIZE; ++i) {
        population[i].tour = (int*)malloc((num_cities + 1) * sizeof(int));
        nearest_neighbor_tsp(cities, num_cities, population[i].tour);
        two_opt(population[i].tour, num_cities, dist);
        population[i].fitness = calculate_fitness(population[i].tour, num_cities, dist);
    }

    for (int generation = 0; generation < GENERATIONS; ++generation) {
        Individual new_population[POP_SIZE];
        for (int i = 0; i < POP_SIZE; ++i) {
            new_population[i].tour = (int*)malloc((num_cities + 1) * sizeof(int));

            int parent1_idx = rand() % POP_SIZE;
            int parent2_idx = rand() % POP_SIZE;
            crossover(population[parent1_idx].tour, population[parent2_idx].tour, new_population[i].tour, num_cities);
            mutate(new_population[i].tour, num_cities);
            new_population[i].fitness = calculate_fitness(new_population[i].tour, num_cities, dist);
        }

        for (int i = 0; i < POP_SIZE; ++i) {
            free(population[i].tour);
            population[i] = new_population[i];
        }
    }

    Individual best_individual = population[0];
    for (int i = 1; i < POP_SIZE; ++i) {
        if (population[i].fitness > best_individual.fitness) {
            best_individual = population[i];
        }
    }

    for (int i = 0; i <= num_cities; ++i) {
        best_tour[i] = best_individual.tour[i];
    }

    for (int i = 0; i < POP_SIZE; ++i) {
        free(population[i].tour);
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

    int* best_tour = (int*)malloc((num_cities + 1) * sizeof(int));
    genetic_algorithm(cities, num_cities, best_tour, dist);

    for (int i = 0; i < num_cities; ++i) {
        free(dist[i]);
    }
    free(dist);
    free(initial_route);

    return best_tour;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input_file>\n", argv[0]);
        return 1;
    }

    srand(time(NULL));

    int num_cities;
    City* cities = read_input(argv[1], &num_cities);

    for (int i = 0; i < num_cities; i++) {
        printf("City %d: x = %f, y = %f\n", i, cities[i].x, cities[i].y);
    }
    printf("Number of cities: %d\n", num_cities);

    int* tour = solve(cities, num_cities);
    print_tour(tour, num_cities);

    free(cities);
    free(tour);

    return 0;
}