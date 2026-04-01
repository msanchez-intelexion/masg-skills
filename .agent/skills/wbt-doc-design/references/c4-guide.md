# Guía C4 Model — Aplicado a Workbeat

## Niveles del C4 Model en Workbeat

### Nivel 1: Contexto del Sistema (toda la plataforma)
Muestra Workbeat como caja negra en su entorno: usuarios, sistemas externos.

### Nivel 2: Contenedores (microservicios)
Descompone la plataforma en sus microservicios y sus tecnologías.

```mermaid
C4Container
    title Workbeat Platform — Nivel 2 Contenedores

    Person(emp, "Empleado", "Usuario final de la superapp")
    Person(admin, "Admin RH", "Configura y reporta")
    Person(integrador, "Integrador", "Conecta sistemas externos")

    System_Boundary(wb, "Workbeat Platform") {
        Container(app, "Superapp Móvil", "React Native", "App del empleado")
        Container(web, "Portal Web", "Angular/React", "Portal administrativo")
        Container(api_adm, "ADM.Api", ".NET 8 / ASP.NET Core", "Core RH endpoints")
        Container(api_crh, "CRH.Api", ".NET 8 / ASP.NET Core", "Comunicación endpoints")
        Container(api_nom, "NOM.Api", ".NET 8 / ASP.NET Core", "Nómina endpoints")
        Container(func, "Azure Functions", ".NET 8 Isolated", "Procesamiento asíncrono")
        ContainerDb(cosmos, "Azure CosmosDB", "NoSQL", "Datos multi-tenant")
        ContainerDb(redis, "Redis Cache", "In-Memory", "Caché L2")
        Container(rmq, "RabbitMQ", "Message Broker", "Bus de eventos")
        Container(blob, "Azure Blob Storage", "Object Storage", "Archivos y multimedia")
    }

    System_Ext(sat, "SAT / IMSS / Infonavit", "Sistemas regulatorios mexicanos")
    System_Ext(idp, "IdentityServer4", "Identity Provider (JWT)")
    System_Ext(cerbos, "Cerbos", "Authorization server (políticas)")
    System_Ext(ai, "OpenAI / Leonardo AI", "Generación de contenido")
```

### Nivel 3: Componentes (internos de un microservicio)

Patrón estándar de cada microservicio Workbeat:

```mermaid
C4Component
    title {Módulo}.Api — Nivel 3 Componentes

    Container_Boundary(api, "{Módulo}.Api") {
        Component(ctrl, "Controllers", "ASP.NET Core", "Endpoints REST, auth, validación")
        Component(svc, "ApplicationService", "C# Class Library", "Lógica de negocio, DTOs")
        Component(domain, "Domain", "C# Class Library", "Entidades, Commands CQRS, Value Objects")
        Component(infra, "Infrastructure", "C# Class Library", "DbContext CosmosDB, RabbitMQ, Redis, BlobStorage")
        Component(common, "Common", "C# Class Library", "Excepciones, DTOs compartidos")
    }

    ContainerDb(cosmos, "CosmosDB", "NoSQL", "Partition: {Año}-{TenantId}")
    ContainerDb(redis, "Redis", "Cache L2")
    Container(rmq, "RabbitMQ")

    Rel(ctrl, svc, "Llama")
    Rel(svc, domain, "Usa entidades y commands")
    Rel(svc, infra, "Persiste y publica")
    Rel(infra, cosmos, "Lee/escribe con EF Core Cosmos")
    Rel(infra, redis, "Lee/escribe caché")
    Rel(infra, rmq, "Publica eventos")
```

## Convenciones de diagrama para Workbeat

### Colores recomendados en Mermaid

```mermaid
graph TB
    A[App / Portal]:::client
    B[API Controller]:::api
    C[ApplicationService]:::service
    D[Domain]:::domain
    E[(CosmosDB)]:::db
    F[(Redis)]:::cache
    G[RabbitMQ]:::messaging
    H[Azure Function]:::function

    classDef client fill:#1168BD,color:#fff
    classDef api fill:#438DD5,color:#fff
    classDef service fill:#85BBF0,color:#000
    classDef domain fill:#F4B942,color:#000
    classDef db fill:#336791,color:#fff
    classDef cache fill:#D82C20,color:#fff
    classDef messaging fill:#FF6600,color:#fff
    classDef function fill:#68A063,color:#fff
```

### Partition Key — siempre documentar

En todo diagrama que involucre CosmosDB, incluir nota:
```
note: Partition Key = "{Año}-{TenantId}"
      Sin partition key → cross-partition scan (⚠️ costoso)
```

### Caché bicapa — patrón estándar

```mermaid
graph LR
    A[Request] --> B{L1: MemoryCache}
    B -->|Hit| C[Response]
    B -->|Miss| D{L2: Redis}
    D -->|Hit| C
    D -->|Miss| E[CosmosDB]
    E --> F[Actualizar L2]
    F --> G[Actualizar L1]
    G --> C
```
