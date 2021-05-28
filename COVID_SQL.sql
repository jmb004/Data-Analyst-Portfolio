-- Pull and view the COVID19 deaths .csv
SELECT *
From portfolioProject..['owid-covid-deaths$']
ORDER BY 3,4

-- Capture non-null continents
SELECT *
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
ORDER BY 3,4

--SELECT *
--FROM portfolioProject..['owid-covid-vac$']
--ORDER BY 3,4

-- SELECT Data that we are going to be using.
SELECT Location, date, total_cases, new_cases, total_deaths, population
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
ORDER BY 1,2

-- Looking at the Total Cases vs Total Deaths (deaths per case %)
-- Shows the liklihood of dying if you contract COVID19 in your country

SELECT Location, date, total_cases, total_deaths, (total_deaths / total_cases)*100 as DeathPercent
FROM portfolioProject..['owid-covid-deaths$']
WHERE location like '%states%' AND continent IS NOT NULL
ORDER BY 1,2


-- Looking at the Total Cases vs Population
-- Shows what % of population in the US got COVID19

SELECT location, date, total_cases, population, (total_cases / population)*100 as ofCasesPerPopulation
FROM portfolioProject..['owid-covid-deaths$']
WHERE location like '%states%'  AND continent IS NOT NULL
ORDER BY 2,3

-- What countries have the highest infection rates?
-- Comparing Population to Infection to gauge spread and containment

SELECT location, population, MAX(total_cases) as HighestInfectionCount, (MAX(total_cases) / population)*100 as InfectionPercent
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY InfectionPercent DESC

-- Let's view counts by Continents
-- Notice issue in dataset mixing Continents in location field. Need to change to drill-down.

SELECT continent, MAX(cast(total_deaths as int)) as TotalDeathCount
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY TotalDeathCount DESC

-- View by location grouped into Continents
-- filter on the nulls in continent to pull Continents out of location

SELECT location, MAX(cast(total_deaths as int)) as TotalDeathCount
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NULL
GROUP BY location
ORDER BY TotalDeathCount DESC


-- Showing the Countries with highest death count per population.
-- Cast the nvarchar255 type to int-type

SELECT location, MAX(cast(total_deaths as int)) as TotalDeathCount, (MAX(total_deaths)/population)*100 as DeathsPerPop
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY TotalDeathCount DESC


-- GLOBAL NUMBERS

-- Total in the World of absolute death percentage
SELECT SUM(new_cases) as TotalCases, SUM(cast(new_deaths as int)) as TotalDeaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
ORDER BY 1,2

-- Total Deaths vs Total Cases by Date
SELECT date, SUM(new_cases) as TotalCases, SUM(cast(new_deaths as int)) as TotalDeaths, SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2

-- Vacination data exploration
SELECT *
FROM portfolioProject..['owid-covid-vac$']

-- Join with Deaths with Vacinations on two things
SELECT *
FROM portfolioProject..['owid-covid-deaths$'] dea
JOIN portfolioProject..['owid-covid-vac$'] vac
ON dea.location = vac.location AND dea.date = vac.date

-- Query on Total Population vs Vaccination
-- Total amount of vaccinations in the world
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations -- new vac's per day
FROM portfolioProject..['owid-covid-deaths$'] dea
JOIN portfolioProject..['owid-covid-vac$'] vac
ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3

-- Query a rolling count of new vacs per day
-- use CONVERT, OVER, and PARTITION BY
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
SUM(CONVERT(int, vac.new_vaccinations)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingVaccinations
FROM portfolioProject..['owid-covid-deaths$'] dea
JOIN portfolioProject..['owid-covid-vac$'] vac
ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3

-- Use CTE to make a Vacination percentage by location
WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingVaccinations)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CONVERT(int,vac.new_vaccinations)) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingVaccinations
	--, (RollingPeopleVaccinated/population)*100
	FROM portfolioProject..['owid-covid-deaths$'] dea
	JOIN portfolioProject..['owid-covid-vac$'] vac
	ON dea.location = vac.location
	AND dea.date = vac.date
	WHERE dea.continent IS NOT NULL

)

SELECT *, (RollingVaccinations/Population)*100 as VacPercentage
FROM PopvsVac


-- TEMP TABLE
-- Drop the temp table

DROP TABLE IF EXISTS #PercentPopulationVaccinated

CREATE TABLE #PercentPopulationVaccinated (
	continent nvarchar(255),
	location nvarchar(255),
	date datetime,
	population numeric,
	new_vaccinations numeric,
	RollingVaccinations int
	)

INSERT INTO #PercentPopulationVaccinated 

	SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CONVERT(int,vac.new_vaccinations)) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingVaccinations
	--, (RollingPeopleVaccinated/population)*100
	FROM portfolioProject..['owid-covid-deaths$'] dea
	JOIN portfolioProject..['owid-covid-vac$'] vac
	ON dea.location = vac.location
	AND dea.date = vac.date
	WHERE dea.continent IS NOT NULL

SELECT *, (RollingVaccinations/Population)*100 as VacPercentage
FROM #PercentPopulationVaccinated

-- CREATE A VIEW 
-- for later visualizatoins

CREATE VIEW PercentPopulationVaccinated AS

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CONVERT(int,vac.new_vaccinations)) OVER (PARTITION BY dea.Location ORDER BY dea.location, dea.Date) AS RollingVaccinations
	FROM portfolioProject..['owid-covid-deaths$'] dea
	JOIN portfolioProject..['owid-covid-vac$'] vac
	ON dea.location = vac.location
	AND dea.date = vac.date
	WHERE dea.continent IS NOT NULL

SELECT *
FROM PercentPopulationVaccinated

-- CREATE A FEW VIEWS

-- Shows what % of population in the US got COVID19
CREATE VIEW TotalCasesvsPopulationView AS

SELECT location, date, total_cases, population, (total_cases / population)*100 as ofCasesPerPopulation
FROM portfolioProject..['owid-covid-deaths$']
WHERE location like '%states%'  AND continent IS NOT NULL

SELECT *
FROM TotalCasesvsPopulation


-- Showing the Countries with highest death count per population.
CREATE VIEW DeathPercentageView AS

SELECT location, MAX(cast(total_deaths as int)) as TotalDeathCount, (MAX(total_deaths)/population)*100 as DeathsPerPop
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
GROUP BY location, population

SELECT *
FROM DeathPercentage

-- Let's view counts by Continents
CREATE VIEW DeathCountView AS

SELECT continent, MAX(cast(total_deaths as int)) as TotalDeathCount
FROM portfolioProject..['owid-covid-deaths$']
WHERE continent IS NOT NULL
GROUP BY continent

SELECT *
FROM DeathCount