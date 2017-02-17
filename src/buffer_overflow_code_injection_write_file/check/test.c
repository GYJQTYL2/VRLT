#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(){
    FILE* fp;           
    fp=fopen("../output/buffer_overflow_code_injection_write_file.txt","r"); 
    if(fp==NULL){
        char buf[]="Do not find file!!!";
        return 0;
    }
    if(fgetc(fp)==EOF){
        char buf[]=" file is null!!!";
        return 0;
    }
    fseek(fp, 0, SEEK_END);
    int file_size;
    file_size = ftell(fp)+1;
    char *tmp;
    fseek(fp, 0, SEEK_SET);
    tmp =  (char *)malloc(file_size * sizeof(char));
    fread(tmp, file_size, sizeof(char), fp);
    tmp[file_size-1]='\0';
    fclose(fp); 
    printf("%s",tmp);
    return 1;
}
