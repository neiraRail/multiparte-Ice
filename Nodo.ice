module Multiparte {
    exception NotReadyError {};

    interface Nodo
    {
        int getMyPart(string s);
        int getPartialSum() throws NotReadyError;
        int getFinalSum() throws NotReadyError;
    }
}