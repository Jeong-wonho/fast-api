<script>
    import fastapi from "../lib/api"
    import {link} from 'svelte-spa-router'

    let question_list = []
    let size = 10
    let page = 0
    let total = 0 
    $: total_page = Math.ceil(total/size)

    function get_question_list(_page) {
        let params = {
            page : _page,
            size : size,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            page = _page
            total = json.total
        })
    }

    get_question_list(0)
</script>

<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="table-dark">
            <th>번호</th>
            <th>제목</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr>
            <td>{i+1}</td>
            <td>
                <a use:link href="/detail/{question.id}">{question.subject}</a>
            </td>
            <td>{question.create_date}</td>
        </tr>
        {/each}
        </tbody>
    </table>
    <ul class="pagination justify-content-center">
        <li class="page-time {page<=0&&'disabled'}">
            <button class="page_link" on:click="{() => get_question_list(page-1)}">이전</button>
        </li>
        <!--페이지번호-->
    </ul>
    <a use:link href="/question-create" class="btn btn-primary">질문 등록 하기</a>
</div>