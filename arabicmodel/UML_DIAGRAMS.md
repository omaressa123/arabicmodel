# UML Diagrams for Arabic Voice-to-Presentation Generator

## Class Diagrams
```plantuml
@startuml
class Presentation {
    +title: String
    +content: String
    +generate(): void
}

class VoiceInput {
    +record(): Audio
    +transcribe(): String
}

class Generator {
    +createPresentation(voice: VoiceInput): Presentation
}

Presentation "1" --> "1..*" VoiceInput
Generator "1" --> "1" Presentation
@enduml
```

## Sequence Diagrams
```plantuml
@startuml
actor User
participant "Voice Input" as VoiceInput
participant "Generator" as Generator
participant "Presentation" as Presentation

User -> VoiceInput: record()
VoiceInput -> VoiceInput: transcribe()
VoiceInput -> Generator: createPresentation(transcript)
Generator -> Presentation: generate()
Presentation -> User: display()
@enduml
```

## Component Diagrams
```plantuml
@startuml
package "Voice Processing" {
    [Voice Input] --> [Transcription Service]
}

package "Presentation Generation" {
    [Generator] --> [Presentation]
}

[Voice Input] --> [Generator]
@enduml
```

## Use Case Diagrams
```plantuml
@startuml
:User: --> (Record Voice)
:User: --> (Generate Presentation)
(Record Voice) --> (Transcribe)
(Generate Presentation) --> (Create Presentation)
@enduml
```

## State Diagrams
```plantuml
@startuml
[*] --> Idle
Idle --> Listening : record()
Listening --> Processing : transcribe()
Processing --> Generating : createPresentation()
Generating --> [*]
@enduml
```

## Deployment Diagrams
```plantuml
@startuml
node "User Device" {
    component "Voice Input"
}

node "Server" {
    component "Transcription Service"
    component "Generator"
    component "Database"
}
@enduml
```

## Data Flow Diagrams
```plantuml
@startuml
actor User
rectangle "Voice Input" as VI
rectangle "Transcription Service" as TS
rectangle "Generator" as G
rectangle "Presentation" as P

User -> VI : record
VI -> TS : send audio
TS -> G : transcribe
G -> P : create presentation
P --> User : display
@enduml
```
