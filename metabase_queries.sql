-- These are the SQL queries for the Metabase dashboard

-- 1. Number of Apprentices by Employer
SELECT employer AS "Employer", COUNT(*) AS "Number of Apprentices"
FROM apprentice_fulfilment
WHERE {{Employer}}
  AND {{Programme}}
  AND {{Onboarding_Status}}
GROUP BY employer
ORDER BY 2 DESC

-- 2. Number of Apprentices by Programme
SELECT programme_name AS "Programme", COUNT(*) AS "Total Candidtes"
FROM apprentice_fulfilment
WHERE {{Employer}} 
  AND {{Programme}}
  AND {{Onboarding_Status}}
  AND programme_name != "Not Applicable"
GROUP BY 1
ORDER BY 2 DESC

-- 3. Number of Apprentices by Onboarding Status
SELECT onboarding_status AS "Onboarding Status", COUNT(*) AS "Total Count"
FROM apprentice_fulfilment
WHERE {{Employer}} 
  AND {{Programme}}
GROUP BY 1

-- 4. Average Days from Nomination to Onboarding
SELECT programme_name AS "Programme Name", 
    AVG(days_to_diagnostic + days_to_assignment + days_to_onboarding) AS "Average Days from Nomination to Onboarding"
FROM apprentice_fulfilment
WHERE {{Employer}} 
  AND {{Programme}}
  AND programme_name != "Not Applicable"
GROUP BY 1
ORDER BY 2 DESC

-- 5. Apprentices by Onboarding Status
SELECT name AS "Name", 
       onboarding_status AS "Onboarding Status", 
       programme_name AS "Programme Name"
FROM apprentice_fulfilment
WHERE {{Employer}} 
  AND {{Programme}} 
  AND {{Onboarding_Status}}
ORDER BY 1 ASC

-- 6. Apprentices by Elapsed Days (randomly chose 31 December 2024 as current date)
SELECT name AS "Name",
       programme_name AS "Programme",
       employer AS "Employer",
       ROUND(JULIANDAY('2460650.26') - JULIANDAY(assigned_date)) AS "Elapsed Days"
FROM apprentice_fulfilment
WHERE {{Employer}} 
  AND {{Programme}}
  AND onboarding_date IS NULL
  AND programme_name != "Not Applicable"
ORDER BY 4 DESC, 1 ASC

-- 7. Apprentices by Coach
SELECT coach_name AS "Coach", COUNT(*) AS "Apprentices Assigned"
FROM apprentice_fulfilment
WHERE {{Employer}} 
  AND {{Programme}} 
  AND {{Onboarding_Status}} 
  AND assigned_date IS NOT NULL
GROUP BY 1
ORDER BY 2 DESC

