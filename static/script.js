// HTML 요소 가져오기
const uploadForm = document.getElementById('uploadForm');
const pdfFile = document.getElementById('pdfFile');
const resultArea = document.getElementById('resultArea');
const downloadLink = document.getElementById('downloadLink');

// 폼 제출 시 이벤트 처리
uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault(); // 폼 기본 동작 방지

    if (!pdfFile.files.length) {
        alert('PDF 파일을 선택해주세요.');
        return;
    }

    const formData = new FormData();
    formData.append('pdfFile', pdfFile.files[0]);

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('파일 변환에 실패했습니다.');
        }

        const data = await response.json();

        // 변환 성공 시 다운로드 링크 출력
        downloadLink.href = data.download_url;
        resultArea.style.display = 'block';

    } catch (error) {
        alert(error.message);
    }
});
