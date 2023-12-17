{
    const fileInput = document.querySelector('#id_profile_pic')
    const profilePic = document.querySelector('.profile .profile-pic')

    function handleChange(e){
        // 사진 파일 가져오기
        const file = e.target.files[0]; // 여러 파일이기 때문에 배열형태 
        if(file){ // 파일이 있을 경우에만 해당 코드를 실행하면 오류가 나지 않는다.
            const fileURL = window.URL.createObjectURL(file); // 임시사진 파일을 저장해주는 공간 
            profilePic.style.backgroundImage = `url(${fileURL})`
        }
       

    }

    fileInput.addEventListener('change',handleChange);
}