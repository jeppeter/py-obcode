#include <stdio.h>

extern int P(void);

int main(int argc,char* argv[])
{
	P();
	printf("%s\n",__FILE__);
	return 0;
}