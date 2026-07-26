-- 1.Total number of images

SELECT COUNT(*) AS total_images
FROM metadata.images;

-- 2.Number of images for each patient

SELECT
    p.patient_id,
    COUNT(i.sop_instance_uid) AS total_images
FROM metadata.patients p
JOIN metadata.studies st
    ON p.patient_id = st.patient_id
JOIN metadata.series se
    ON st.study_uid = se.study_uid
JOIN metadata.images i
    ON se.series_uid = i.series_uid
GROUP BY p.patient_id
ORDER BY total_images DESC;

-- 3.Images grouped by scanner manufacturer

SELECT
    manufacturer,
    COUNT(*) AS total_images
FROM metadata.images
GROUP BY manufacturer
ORDER BY total_images DESC;

-- 4.Number of images by imaging modality

SELECT
    s.modality,
    COUNT(*) AS total_images
FROM metadata.series s
JOIN metadata.images i
    ON s.series_uid = i.series_uid
GROUP BY s.modality;

-- 5.Average slice thickness

SELECT
    ROUND(AVG(slice_thickness),2) AS average_slice_thickness
FROM metadata.images;

-- 6.Average image dimensions

SELECT
    ROUND(AVG(rows),0) AS average_rows,
    ROUND(AVG(columns),0) AS average_columns
FROM metadata.images;

-- 7.Number of studies for each patient

SELECT
    patient_id,
    COUNT(*) AS total_studies
FROM metadata.studies
GROUP BY patient_id;

-- 8.Number of series for each study

SELECT
    study_uid,
    COUNT(*) AS total_series
FROM metadata.series
GROUP BY study_uid;

-- 9.Scanner manufacturers used for each patient

SELECT
    p.patient_id,
    i.manufacturer,
    COUNT(*) AS total_images
FROM metadata.patients p
JOIN metadata.studies st
    ON p.patient_id = st.patient_id
JOIN metadata.series se
    ON st.study_uid = se.study_uid
JOIN metadata.images i
    ON se.series_uid = i.series_uid
GROUP BY
    p.patient_id,
    i.manufacturer
ORDER BY
    p.patient_id;

-- 10.Patients with the highest number of images

SELECT
    p.patient_id,
    COUNT(*) AS image_count
FROM metadata.patients p
JOIN metadata.studies st
    ON p.patient_id = st.patient_id
JOIN metadata.series se
    ON st.study_uid = se.study_uid
JOIN metadata.images i
    ON se.series_uid = i.series_uid
GROUP BY p.patient_id
ORDER BY image_count DESC
LIMIT 5;