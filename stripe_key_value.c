#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

#define MAXN 10
typedef struct tree_s
{
	char s[MAXN+1];
	int value;
	struct tree_s * lt;
	struct tree_s * gt;
} TREE_T;

TREE_T *tree_new(char *name)
{
	TREE_T *t=calloc(sizeof(TREE_T),1);
	assert(t);
	strcpy(t->s,name);
	return t;
}

void tree_free(TREE_T *t)
{
	if (t==NULL) return;
	tree_free(t->lt);
	tree_free(t->gt);
	free(t);
}




/*
This may be too slow because the tree could end up very unbalanced if presented in alphabetical order.
Probably better to switch to C++ and use STL.
Or could hash the strings first.
Or use a balancing data structure.
*/
TREE_T *tree_get(TREE_T *t,char *name)
{
	int x=strcmp(name,t->s);
	if (x==0) return t;
	if (x<0)
	{
		if (!t->lt) t->lt=tree_new(name);
		return tree_get(t->lt,name);
	}
	if (!t->gt) t->gt=tree_new(name);
	return tree_get(t->gt,name);
}

/* Returns tree if it exists, or NULL otherwise */
TREE_T *tree_has(TREE_T *t,char *name)
{
	int x=strcmp(name,t->s);
	if (x==0) return t;
	if (x<0)
	{
		if (!t->lt) return NULL;
		return tree_has(t->lt,name);
	}
	if (!t->gt) return NULL;
	return tree_has(t->gt,name);
}

// File format is int N for length of string (0 if null), string, value, left stuff right stuff

TREE_T *tree_rload(FILE *fid)
{
	int n=0;
	TREE_T *t=NULL;
	fread(&n,sizeof(n),1,fid);
	if (n==0) return t;
	assert(n<=MAXN);
	char p[MAXN+1];
	fread(p,n,1,fid);
	p[n]=0;
	t=tree_new(p);
	fread(&t->value,sizeof(t->value),1,fid);
	t->lt=tree_rload(fid);
	t->gt=tree_rload(fid);
	return t;
}

TREE_T *tree_load(void)
{
	FILE *fid=fopen("/tmp/peter","rb");
	if (fid==NULL)
	{
		return tree_new("m for back");
	}
	TREE_T *t=tree_rload(fid);
	fclose(fid);
	return t;
}

void tree_rsave(FILE *fid, TREE_T *t)
{
	int n=0;
	if (t)
		n=strlen(t->s);
	fwrite(&n,sizeof(n),1,fid);
	if (n==0) return;
	fwrite(t->s,n,sizeof(char),fid);
	fwrite(&t->value,sizeof(t->value),1,fid);
	tree_rsave(fid,t->lt);
	tree_rsave(fid,t->gt);
	free(t);
}

void tree_save(TREE_T *t)
{
	FILE *fid=fopen("/tmp/peter","wb");
	assert(fid);
	tree_rsave(fid,t);
	fclose(fid);
}

/* Write all entries in t into the backup tree and free storage*/
void tree_commit(TREE_T *backup,TREE_T *t)
{
	if (t==NULL) return;
	TREE_T *b=tree_get(backup,t->s);
	b->value=t->value;
	tree_commit(backup,t->lt);
	tree_commit(backup,t->gt);
	free(t);
}

 void keyValue(char a[][30] ,int n) {
	int i;
	TREE_T *root=tree_new("m for root");
	TREE_T *backup=tree_load();
	for(i=0;i<n;i++)
	{
		char *p=a[i];
		int value;
		char name[MAXN+1];
		TREE_T *t;
		switch(p[0])
		{
		case 'S':
			sscanf(p,"SET %s %d",&name,&value);
			t=tree_get(root,name);
			t->value=value;
			break;
		case 'G':
			sscanf(p,"GET %s",&name);
			t=tree_has(root,name);
			if (!t)
				t=tree_get(backup,name);
			printf("%d\n",t->value);
			break;
		case 'R':
			tree_free(root);
			root=tree_new("m for root");
			break;
		case 'C':
			tree_commit(backup,root);
			root=tree_new("m for root");
			break;
		default:
			assert(0);
		}
	}
	tree_free(root);
	tree_save(backup);
}

int main (int argc,char *argv[])
{
        char d1[][30]={"SET a 1","SET b 2","GET a","COMMIT","SET b 3"};
	char d2[][30]={"GET b","SET b 4"};
	char d3[][30]={"GET b"};
	keyValue(d1,5);
	keyValue(d2,2);
	keyValue(d3,1);
	return 0;
}
