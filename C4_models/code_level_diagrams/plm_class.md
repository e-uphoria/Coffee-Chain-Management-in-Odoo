```mermaid
classDiagram
    class Document {
        +id
        +name
        +type
        +file
    }
    class Revision {
        +id
        +document_id
        +version
        +status
    }
    class Approval {
        +id
        +revision_id
        +approver
        +status
    }

    Document "1" --> "0..*" Revision
    Revision "1" --> "0..1" Approval
