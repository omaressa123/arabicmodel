let mediaRecorder;
let chunks = [];

const btn = document.getElementById("mic-btn");
const status = document.getElementById("status");
const results = document.getElementById("results");
const processingStep = document.getElementById("processing-step");
const downloadContainer = document.getElementById("download-container");
const downloadLink = document.getElementById("download-link");

btn.onclick = async () => {
    if (!mediaRecorder || mediaRecorder.state === "inactive") {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = e => {
                chunks.push(e.data);
            };

            mediaRecorder.onstop = async () => {
                const blob = new Blob(chunks, { type: 'audio/webm' });
                chunks = [];
                
                // Show loading state
                status.innerText = "اكتمل التسجيل. جاري الرفع...";
                results.classList.remove("hidden");
                processingStep.innerText = "جاري رفع الصوت ومعالجته...";
                downloadContainer.classList.add("hidden");

                // Automatically upload to server
                await uploadAudio(blob);
            };

            mediaRecorder.start();
            btn.classList.add("recording");
            status.innerText = "جاري التسجيل... انقر مرة أخرى للتوقف";
            results.classList.add("hidden");
        } catch (err) {
            console.error("Error accessing microphone:", err);
            status.innerText = "خطأ: تعذر الوصول للميكروفون";
        }
    } else {
        mediaRecorder.stop();
        btn.classList.remove("recording");
        status.innerText = "تم إيقاف التسجيل. جاري المعالجة...";
    }
};

async function uploadAudio(blob) {
    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            status.innerText = "تم الانتهاء بنجاح!";
            processingStep.innerText = "اكتملت المعالجة!";
            downloadContainer.classList.remove("hidden");
            downloadLink.href = data.download_url;
            downloadLink.innerText = "تحميل العرض التقديمي (PPTX)";
        } else {
            status.innerText = "خطأ في المعالجة";
            processingStep.innerText = "حدث خطأ: " + (data.error || "فشل غير معروف");
        }
    } catch (err) {
        console.error("Error uploading audio:", err);
        status.innerText = "خطأ في الاتصال بالخادم";
        processingStep.innerText = "تعذر الاتصال بالخادم";
    }
}
