<script>
  import fastapi from "../lib/api";
  import { link } from "svelte-spa-router";
  import { page, is_login } from "../lib/store";
  import moment from "moment";
  import "moment/locale/ko";
  moment.locale("ko");

  let question_list = [];
  let size = 10;
  let total = 0;
  // const maxButton = 10;
  let start = 0;
  let kw = "";

  $: total_page = Math.ceil(total / size);

  function get_question_list(_page) {
    if (_page < 0) {
      _page = 0;
    }

    if (_page > total_page && total_page > 0) {
      _page = total_page - 1;
    }
    let params = {
      page: _page,
      size: size,
      keyword: kw,
    };
    fastapi("get", "/api/question/list", params, (json) => {
      question_list = json.question_list;
      $page = _page;
      total = json.total;
    });

    start = Math.floor(_page / 10) * 10;
  }

  $: get_question_list($page);

  function customRange(start, stop, total_page) {
    //보여지는것이다.
    if (start < 0) {
      start = 0;
    }

    if (stop > total_page) {
      stop = total_page;
    }
    return Array.from({ length: stop - start }, (_, i) => i + start);
  }
</script>

<div class="container my-3">
  <div class="row my-3">
    <div class="col-6">
      <a
        use:link
        href="/question-create"
        class="btn btn-primary {$is_login ? '' : 'disabled'}">질문 등록하기</a
      >
    </div>
    <div class="col-6">
      <div class="input-group">
        <input type="text" class="form-control" bind:value={kw} />
        <button
          class="btn btn-outline-secondary"
          on:click={() => get_question_list(0)}>찾기</button
        >
      </div>
    </div>
  </div>
  <table class="table">
    <thead>
      <tr class="text-center table-dark">
        <th>번호</th>
        <th style="width:50%">제목</th>
        <th>글쓴이</th>
        <th>작성일시</th>
      </tr>
    </thead>
    <tbody>
      {#each question_list as question, i}
        <tr class="text-center">
          <td>{total - $page * size - i}</td>
          <td class="text-start">
            <a use:link href="/detail/{question.id}">{question.subject}</a>

            {#if question.answers.length > 0}
              <span class="text-danger small mx-2"
                >{question.answers.length}</span
              >
            {/if}
          </td>
          <td>{question.user ? question.user.username : ""}</td>
          <td
            >{moment(question.create_date).format(
              "YYYY년 MM월 DD일 hh:mm a"
            )}</td
          >
        </tr>
      {/each}
    </tbody>
  </table>

  <!-- 페이징 처리 시작 -->
  <ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {$page <= 0 && 'disabled'}">
      <button class="page-link" on:click={() => get_question_list($page - 10)}
        >이전</button
      >
    </li>
    <!--페이지번호-->

    {#each customRange(start, start + 10, total_page) as loop_page}
      <!-- {#if loop_page >= page-5 && loop_page <= total_page}  -->
      <li class="page-item {loop_page === $page && 'active'}">
        <button on:click={() => get_question_list(loop_page)} class="page-link"
          >{loop_page + 1}</button
        >
      </li>
      <!-- {/if} -->
    {/each}
    <!--다음페이지-->
    <li class="page-item {$page >= total_page - 1 && 'disabled'}">
      <button class="page-link" on:click={() => get_question_list($page + 10)}
        >다음</button
      >
    </li>
  </ul>

</div>
