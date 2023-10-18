module ZIceComms {
    exception NodoError {
        string reason;
    };

    interface Nodo
    {
        string get(string key, int id) throws NodoError; //Metodo para solicitar la parte que le corresponda al solicitante
        bool post(string key, string payload, int id) throws NodoError;
    }
}