#include <stdio.h>

/*
Esta é a função que será "exportada" para o Python.
Ela recebe a NOTA (que será a média calculada pelo Python) e as FALTAS.
*/
const char* calcular_status(float nota, int faltas) {
    
 
    
    if (faltas > 15) { 
        return "Reprovado (Falta)";
    }

    if (nota >= 7.0) { 
        return "Aprovado";
    } else {
        return "Reprovado (Nota)";
    }
}
