/*
  gcc -fPIC -shared buffer_overflow_code_injection_write_file.c -o buffer_overflow_code_injection_write_file.so
  
*/

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

char* check(){
    FILE* fp;
    char *buf;   
    buf =  (char *)malloc(200 * sizeof(char));  
    strcpy(buf,getenv("OUTPUT_buffer_overflow_code_injection_write_file_PATH"));
    strcat(buf,".txt");      
    fp=fopen(buf,"r"); 
    if(fp==NULL){
        strcpy(buf,"attack fail, Do not find buffer_overflow_code_injection_write_file.txt file !!!\n");
        return buf;
    }
    if(fgetc(fp)==EOF){
        strcpy(buf,"attack fail, file is null !!!\n");
        return buf;
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
    return tmp;
}

