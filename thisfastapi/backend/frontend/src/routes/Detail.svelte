<script>
  // @ts-nocheck

  import fastapi from "../lib/api";
  import Error from "../components/Error.svelte";
  import { link, push } from "svelte-spa-router";
  import { is_login, username } from "../lib/store";
  import { marked } from "marked";
  import moment from "moment";
  import "moment/locale/ko";

  moment.locale("ko");

  export let params = {};
  let question_id = params.question_id;
  let question = { answers: [], voter: [] , content: ''};
  let content = "";
  let error = { detail: [] };
  const itemsPerPage = 5;
  let currentPage = 1; 
  let totalPage = 0;
  let startIndex= (currentPage-1) * itemsPerPage;
  let endIndex= startIndex + itemsPerPage;


// 이전 페이지로 이동하는 함수
  function previousPage() {
    currentPage--;
    updateIndexes();
  }
// 다음 페이지로 이동하는 함수
  function nextPage() {
    currentPage++;
    updateIndexes();
  } 
  function goToPage(pageNumber) {
    currentPage = pageNumber;
    updateIndexes();
  }

  // 시작 인덱스와 끝 인덱스를 업데이트하는 함수
  function updateIndexes() {
    startIndex = (currentPage -1) * itemsPerPage;
    endIndex= startIndex + itemsPerPage;
  }
  
  /** 질문과 답변 받아오는 함수*/
  function get_question() {
    fastapi("get", "/api/question/detail/" + question_id, {}, (json) => {
      question = json;
      totalPage = Math.ceil(question.answers.length/ itemsPerPage);
    });
  }
  get_question();

  /**
   * 질의 등록 함수
   * @param event 질문등록 이벤트 발생
   */
  function post_answer(event) {
    event.preventDefault();
    let url = "/api/answer/create/" + question_id;
    let params = {
      content: content,
    };
    fastapi(
      "post",
      url,
      params,
      (json) => {
        content = "";
        error = { detail: [] };
        get_question();
      },
      (err_json) => {
        error = err_json;
      }
    );
  }
  /**
   * 질문삭제
   * @param _question_id : 질의 아이디 입력
   */
  function delete_question(_question_id) {
    if (window.confirm("정말로 삭제하시겠습니까?")) {
      let url = "/api/question/delete";
      let params = {
        question_id: _question_id,
      };
      fastapi(
        "delete",
        url,
        params,
        (json) => {
          push("/");
        },
        (err_json) => {
          error: err_json;
        }
      );
    }
  }
  /**
   * 질의문 삭제
   * @param answer_id 질문 id
   */
  function delete_answer(answer_id) {
    if (window.confirm("정말로 삭제하시겠습니까?")) {
      let url = "/api/answer/delete";
      let params = {
        answer_id: answer_id,
      };
      fastapi(
        "delete",
        url,
        params,
        (json) => {
          get_question();
        },
        (err_json) => {
          error = err_json;
        }
      );
    }
  }
  /**
   * 질문 추천 함수
   * @param _question_id 질의 아이디를 보고 추천
   */
  function vote_question(_question_id) {
    if (window.confirm("정말로 추천하시겠어요?")) {
      let url = "/api/question/vote";
      let params = {
        question_id: _question_id,
      };
      fastapi(
        "post",
        url,
        params,
        (json) => {
          get_question();
        },
        (err_json) => {
          error = err_json;
        }
      );
    }
  }
  /**
   * 질문 추천 함수
   * @param answer_id answerId에 따른
   */
  function vote_answer(answer_id) {
    if (window.confirm("정말로 추천하시겠습니까?")) {
      let url = "/api/answer/vote";
      let params = {
        answer_id: answer_id,
      };
      fastapi(
        "post",
        url,
        params,
        (json) => {
          get_question();
        },
        (err_json) => {
          error = err_json;
        }
      );
    }
  }
</script>

<div class="container my-3">
  <!-- 질문 -->
  <h2 class="border-bottom py-2">{question.subject}</h2>
  <div class="card my-3">
    <div class="card-body">
      <div class="card-text">
        {@html marked.parse(question.content)}
      </div>
      <div class="d-flex justify-content-end">
        {#if question.modify_date}
          <div class="badge bg-light text-dark p-2 text-start mx-3">
            <div class="mb-2">modified at</div>
            <div>
              {moment(question.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}
            </div>
          </div>
        {/if}
        <div class="badge bg-light text-dark p-2 text-start">
          <div class="mb-2">{question.user ? question.user.username : ""}</div>
          <div>
            {moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
          </div>
        </div>
      </div>
      <div class="my-3">
        <button
          class="btn btn-sm btn-outline-secondary"
          on:click={vote_question(question.id)}
          >추천<span class="badge rounded-pill bg-success"
            >{question.voter.length}</span
          ></button
        >
        {#if question.user && $username === question.user.username}
          <a
            use:link
            href="/question-modify/{question.id}"
            class="btn btn-sm btn-outline-secondary">수정</a
          >
          <button
            class="btn btn-sm btn-outline-secondary"
            on:click={() => delete_question(question.id)}>삭제</button
          >
        {/if}
      </div>
    </div>
  </div>
  <!-- 목록 버튼 추가-->
  <button
    class="btn btn-secondary"
    on:click={() => {
      push("/");
    }}>목록으로</button
  >
  <!-- 답변 목록 -->
  <h5 class="border-bottom my-3 py-2">
    {question.answers.length}개의 답변이 있습니다.
  </h5>
  {#each question.answers.slice(startIndex, endIndex) as answer}
    <div class="card my-3">
      <div class="card-body">
        <div class="card-text">
          {@html marked.parse(answer.content)}
        </div>
        <div class="d-flex justify-content-end">
          {#if answer.modify_date}
            <div class="badge bg-light text-dark p-2 text-start mx-3">
              <div class="mb-2">modified at</div>
              <div>
                {moment(answer.modify_date).format("YYYY년 MM월 DD일 hh:mm a")}
              </div>
            </div>
          {/if}
          <div class="badge bg-light text-dark p-2 text-start">
            <div class="mb-2">{answer.user ? answer.user.username : ""}</div>
            <div>
              {moment(answer.create_date).format("YYYY년 MM월 DD일 hh:mm a")}
            </div>
          </div>
        </div>
        <div class="my-3">
          <button
            class="btn btn-sm btn-outline-secondary"
            on:click={vote_answer(answer.id)}
          >
            추천
            <span class="badge rounded-pill bg-success"
              >{answer.voter.length}</span
            >
          </button>
          {#if answer.user && $username === answer.user.username}
            <a
              use:link
              href="/answer-modify/{answer.id}"
              class="btn btn-sm btn-outline-secondary">수정</a
            >
            <button
              class="btn btn-sm btn-outline-secondary"
              on:click={() => delete_answer(answer.id)}>삭제</button
            >
          {/if}
        </div>
      </div>
    </div>
  {/each}

   <!-- 페이징 처리 시작 -->
   <ul class="pagination justify-content-center">
    <!-- 이전페이지 -->
    <li class="page-item {currentPage <= 1 && 'disabled'}">
      <button class="page-link" on:click={() => previousPage(currentPage)}
        >이전</button
      >
    </li>
    <!--페이지번호-->
    {#each Array(totalPage).fill().map((_,i) => i + 1) as page}
      <li class="page-item {page === currentPage && 'active'}">
        <button on:click={() => goToPage(page)} class="page-link"
          >{page}</button
        >
      </li>
    {/each}
    <!--다음페이지-->
    <li class="page-item {currentPage >= totalPage && 'disabled'}">
      <button class="page-link" on:click={() => nextPage(currentPage + 10)}
        >다음</button
      >
    </li>
  </ul>
  <!-- 답변 등록 -->
  <Error {error} />
  <form method="post" class="my-3">
    <div class="mb-3">
      <textarea
        rows="10"
        bind:value={content}
        disabled={$is_login ? "" : "disabled"}
        class="form-control"
      />
    </div>
    <input
      type="submit"
      value="답변등록"
      class="btn btn-primary {$is_login ? '' : 'disabled'}"
      on:click={post_answer}
    />
  </form>
</div>
