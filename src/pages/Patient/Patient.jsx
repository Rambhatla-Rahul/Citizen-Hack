import React, { useState } from 'react';

const apiUrl = 'http://192.168.106.190:8000'; 

const Patient = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysisResults, setAnalysisResults] = useState(null); // Store analysis results here

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    const reader = new FileReader();
    reader.onload = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };
  

  const handleGenerateReport = async () => {
    setLoading(true);
    setAnalysisResults(null); // Clear previous results

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const uploadResponse = await fetch(`${apiUrl}/upload-image`, {
        method: 'POST',
        body: formData,
      });

      const uploadData = await uploadResponse.json();
      if (uploadResponse.ok) {
        // Extract and set the analysis results
        setAnalysisResults(uploadData.results); 
      } else {
        setAnalysisResults({ error: uploadData.error || 'Error uploading image.' });
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      setAnalysisResults({ error: 'Error uploading image.' });
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div className="flex w-full h-full">
      <div className="w-full h-full flex flex-col justify-center items-center mt-10 mb-10">
        {!imagePreview && (
          <img src='../../../public/assets/how_to_do.jpg' alt='hot-to-use' className='w-[1050px] h-[500px] border-2 border-black border-solid'/>
        )}
        {imagePreview && (
          <img src={imagePreview} alt="image preview" className="w-[450px] h-[600px] mb-4" />
        )}
        {loading && <div className="mt-10 text-gray-500 font-bold text-2xl mb-8">
            Generating... (May take upto a minute)
                
          </div>}
        <div className="flex justify-space-between items-center gap-20 mt-20">
          <button
            onClick={() => document.getElementById('file-input').click()}
            className="mt-[8px] border-black border-2 rounded-xl p-2 font-bold h-[50px]"
            id="upload-btn"
          >
            Upload Report
          </button>

          {imagePreview && (
            <button
              onClick={handleGenerateReport}
              className="mt-[8px] border-black border-2 rounded-xl p-2 font-bold h-[50px]"
              id="generate-btn"
            >
              Generate Report
            </button>
          )}
        </div>

        <input
          type="file"
          id="file-input"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />

        

        {/* Display Analysis Results */}
        {analysisResults && (
          <div className="mt-20 w-[1000px] bg-white p-4 text-lg font-bold text-center mb-10 " id= 'analysis-container'>
            {analysisResults.error ? (
              <p className="text-red-500">{analysisResults.error}</p>
            ) : (
              <div className='flex  flex-col gap-8'>
                <h3 className="text-3xl font-bold">Analysis Results:</h3>
                <hr className='border-black'/>
                <p className='flex items-start'><strong>Summary:</strong> <br/>{analysisResults.summary}</p>
                <p className='flex items-start'><strong>Translation:</strong> <br/>{analysisResults.translation}</p>
                <p className='flex items-start'><strong className='mr-8'>Anamoly: </strong> <br/>{analysisResults.anamoly}</p>
                <p className='flex items-start'><strong className='mr-3'>Root Cause:</strong> <br/>{analysisResults.root_cause}</p>
                <p className='flex items-start mb-8'><strong className='mr-3'>Root Cause 1:</strong> <br/>{analysisResults.root_cause_1}</p>
                
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Patient;
