module Multiparte {
    exception NotReadyError {};

    interface Nodo
    {
        int getMyPart(string s); //Metodo para solicitar la parte que le corresponda al solicitante
        int getPartialSum() throws NotReadyError; //Metodo para solicitar la suma parcial de este nodo
        int getFinalSum() throws NotReadyError; // Metodo para solicitar la suma final
    }
}