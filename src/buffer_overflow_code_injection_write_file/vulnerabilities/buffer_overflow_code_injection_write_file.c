/*gcc -fno-stack-protector -z execstack -g -o buffer_overflow_code_injection_write_file buffer_overflow_code_injection_write_file.c 
  dep aslr off
*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
FILE* g_fp; 

void read_file(){
    char buf[200];
    int v,length=0; 
    if(strcmp(getenv("ATTACH"),"TRUE")==0)
        getchar();
    strcpy(buf,getenv("INPUT_buffer_overflow_code_injection_write_file_PATH"));
    if(strcmp(getenv("NORMAL"),"TRUE")==0)
        strcat(buf,"_normal.txt");
    else
        strcat(buf,".txt");
    g_fp=fopen(buf,"r"); 
    if(g_fp==NULL)
    {
        printf("open file failed!\n");
        exit(1);
    }
    strcpy(buf,"");
    while (fscanf(g_fp, "\\x%02x", &v) == 1)
    {   
        buf[length++] = v;
    } 
    fclose(g_fp);
}

int main(int argc,char *argv[]){
    read_file(); 
    printf("normal program!!\n");
    return 0;
}
