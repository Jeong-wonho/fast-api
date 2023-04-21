<script>
  import fastapi from "../lib/api";

    export let params = {}
    let question_id = params.question_id
    
    let question = {}

    function get_schema() {
        fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
            question = json
        })
    }


    get_schema()
</script>

<h1>{question.subject}</h1>
<div>
    {question.content}
</div>