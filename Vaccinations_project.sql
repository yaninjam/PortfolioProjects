select * 
from PortfolioProject..CovidDeaths
where continent is not null
order by 3,4

--select * 
--from PortfolioProject..CovidVaccinations
--order by 3,4

--select data to use
select location, date, total_cases, new_cases, total_deaths, population
from PortfolioProject..CovidDeaths
where continent is not null
order by 1, 2

--Total cases vs total deaths
--Shows the likelihood of dying if you contract covid in Australia
select location, date, total_cases, total_deaths, (CAST(total_deaths AS float) / CAST(total_cases AS float)) * 100 AS DeathPercentage
from PortfolioProject..CovidDeaths
where location = 'Australia'
order by 1, 2

--Total cases vs Population
--Shows what percentage of population got covid
select location, date, total_cases, population, (total_cases /population) * 100 AS CovidPercentage
from PortfolioProject..CovidDeaths
--where location = 'Australia'
where continent is not null
order by 1, 2

--Countries with highest infection rate companred to population
select location, max(total_cases) as HighestInfectionCount, population, max((total_cases /population)) * 100 AS PercentPopulationInfected
from PortfolioProject..CovidDeaths
--where location = 'Australia'
where continent is not null
group by location, population
order by PercentPopulationInfected desc

--Showing countries with highest death count per population
select location, max(cast(total_deaths as int)) as TotalDealthCount
from PortfolioProject..CovidDeaths
--where location = 'Australia'
where continent is not null
group by location
order by TotalDealthCount desc

--Break things down by continent


--Showing the continents with the highest count per population
select continent, max(cast(total_deaths as int)) as TotalDealthCount
from PortfolioProject..CovidDeaths
--where location = 'Australia'
where continent is not null
group by continent
order by TotalDealthCount desc

--Global numbers
select sum(new_cases) as total_cases, sum(cast(new_deaths as int)) as total_deaths, sum(CAST(new_deaths AS int)) / NULLIF(sum(new_cases), 0) * 100 AS DeathPercentage
from PortfolioProject..CovidDeaths
--where location = 'Australia'
where continent is not null
--group by date
order by 1, 2


-- Use CTE
with PopvsVac (Continent, Location, Date, Population, New_vaccinations, RollingPeopleVaccinated)
as
(
--Total population vs vaccinations
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3
)
select *, (RollingPeopleVaccinated/population)*100
from PopvsVac;



--Temp table

drop table if exists #PercentPopulationVaccinated
create table #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime, 
population numeric, 
new_vaccinations numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
order by 2,3

select *, (RollingPeopleVaccinated/population)*100
from #PercentPopulationVaccinated;

--creating view to store data for later visualisations
create view PercentPopulationVaccinated as
select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, sum(convert(bigint, vac.new_vaccinations)) over (partition by dea.location order by dea.location, dea.date) as RollingPeopleVaccinated
--, (RollingPeopleVaccinated/population)*100
from PortfolioProject..CovidDeaths dea
join PortfolioProject..CovidVaccinations vac
	on dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null
--order by 2,3


Select * 
From PercentPopulationVaccinated