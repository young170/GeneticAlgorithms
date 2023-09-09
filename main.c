#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

struct _constraint {
	int length;
};

int ** init_population (struct * constraint);

int main (int argc, char *argv[]) {
	int len, var, size;
	int opt;

	len = 0;
	var = 0;
	while ((opt = getopt(argc, argv, "")) != -1) {
		switch(opt) {
			case 'l':
				len = atoi(optarg);
				break;
			case 'v':
				var = atoi(optarg);
				break;
			case 's':
				size = atoi(optarg);
			default:
				fprintf(stderr, "Usage: %s [-l length] [-v variation] [-s size]", argv[0]);
				exit(EXIT_FAILURE);
		}
	}

	struct _constraint * constraint = (struct _constraint *) malloc(sizeof(struct _constraint));
	// init_population
	int ** population = init_population(constraint);
	// crossover
	// selection
	// termination
	return 0;	
}
