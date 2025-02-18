# Documentazione dell'API

## Introduzione
Questa documentazione descrive le API disponibili per l'interazione con il sistema OpenPSA. Le API sono progettate per essere semplici da usare e flessibili per soddisfare diverse esigenze.

## Autenticazione
Per utilizzare le API, è necessario autenticarsi utilizzando un token API. Il token deve essere incluso nell'intestazione di ogni richiesta.

### Esempio di intestazione
```
Authorization: Bearer <tuo_token_api>
```

## Endpoints

### 1. Ottieni tutti i progetti
**Endpoint:** `/api/progetti`  
**Metodo:** `GET`  
**Descrizione:** Recupera una lista di tutti i progetti.

#### Parametri
- `status` (opzionale): Filtra i progetti per stato (`attivo`, `completato`, `in_attesa`).

#### Esempio di richiesta
```
GET /api/progetti?status=attivo
```

#### Esempio di risposta
```json
[
    {
        "id": 1,
        "nome": "Progetto Alpha",
        "descrizione": "Descrizione del progetto Alpha",
        "stato": "attivo"
    },
    {
        "id": 2,
        "nome": "Progetto Beta",
        "descrizione": "Descrizione del progetto Beta",
        "stato": "completato"
    }
]
```

### 2. Crea un nuovo progetto
**Endpoint:** `/api/progetti`  
**Metodo:** `POST`  
**Descrizione:** Crea un nuovo progetto.

#### Corpo della richiesta
```json
{
    "nome": "Nome del progetto",
    "descrizione": "Descrizione del progetto"
}
```

#### Esempio di risposta
```json
{
    "id": 3,
    "nome": "Nome del progetto",
    "descrizione": "Descrizione del progetto",
    "stato": "attivo"
}
```

### 3. Aggiorna un progetto
**Endpoint:** `/api/progetti/{id}`  
**Metodo:** `PUT`  
**Descrizione:** Aggiorna le informazioni di un progetto esistente.

#### Corpo della richiesta
```json
{
    "nome": "Nome aggiornato del progetto",
    "descrizione": "Descrizione aggiornata del progetto",
    "stato": "completato"
}
```

#### Esempio di risposta
```json
{
    "id": 1,
    "nome": "Nome aggiornato del progetto",
    "descrizione": "Descrizione aggiornata del progetto",
    "stato": "completato"
}
```

### 4. Elimina un progetto
**Endpoint:** `/api/progetti/{id}`  
**Metodo:** `DELETE`  
**Descrizione:** Elimina un progetto esistente.

#### Esempio di risposta
```json
{
    "message": "Progetto eliminato con successo"
}
```

## Errori comuni
- `401 Unauthorized`: Token API non valido o mancante.
- `404 Not Found`: Risorsa non trovata.
- `400 Bad Request`: Richiesta malformata o parametri mancanti.

## Contatti
Per ulteriori informazioni o supporto, contattare il team di sviluppo all'indirizzo email: supporto@openpsa.com.
