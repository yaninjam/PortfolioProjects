Select *
From PortfolioProject.dbo.NashvilleHousing
------------------------------------------------------------------------------------------------------------------------------------
-- Standardise date format

Select CONVERT(date, SaleDate) as SaleDateConverted
From PortfolioProject.dbo.NashvilleHousing

------------------------------------------------------------------------------------------------------------------------------------
-- update the null values in the PropertyAddress column of the NashvilleHousing table with non-null values from matching rows that have the same ParcelID but different UniqueID
Select PropertyAddress
From PortfolioProject.dbo.NashvilleHousing

Select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject.dbo.NashvilleHousing as a
Join PortfolioProject.dbo.NashvilleHousing as b
	on a.ParcelID = b.ParcelID -- ParcelID is the same
	and a.[UniqueID ] <> b.[UniqueID ] -- but UniqueID is different, because of different row

update a
set PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
From PortfolioProject.dbo.NashvilleHousing as a
Join PortfolioProject.dbo.NashvilleHousing as b
	on a.ParcelID = b.ParcelID -- ParcelID is the same
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

------------------------------------------------------------------------------------------------------------------------------------

-- Split Propertyddress into individual columns (address, city, state)
Select PropertyAddress
From PortfolioProject.dbo.NashvilleHousing

select 
SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) -1) as Address --  extracts the portion of the address from the beginning until the first comma (,), excluding the comma itself
, SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) +1, len(PropertyAddress)) as Address -- extracts the portion of the address starting from the character right after the first comma (,), until the end of the string


Select CONVERT(date, SaleDate) as SaleDateConverted
From PortfolioProject.dbo.NashvilleHousing

------------------------------------------------------------------------------------------------------------------------------------

-- Alter column from PropertyAddress
alter table NashvilleHousing
add PropertySplitAddress Nvarchar(255);

Update NashvilleHousing
set PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) -1)

alter table NashvilleHousing
add PropertySplitCity Nvarchar(255);

Update NashvilleHousing
set PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) +1, len(PropertyAddress))

Select * 
From PortfolioProject.dbo.NashvilleHousing

Select OwnerAddress 
From PortfolioProject.dbo.NashvilleHousing

------------------------------------------------------------------------------------------------------------------------------------

-- Split OwnerAddress
Select
PARSENAME(Replace(OwnerAddress, ',', '.'), 3)  --  replace the commas (,) with period (.) and extracts the third part
, PARSENAME(Replace(OwnerAddress, ',', '.'), 2) --  replace the commas (,) with period (.) and extracts the second part
, PARSENAME(Replace(OwnerAddress, ',', '.'), 1) --  replace the commas (,) with period (.) and extracts the first part

From PortfolioProject.dbo.NashvilleHousing

------------------------------------------------------------------------------------------------------------------------------------

-- Alter column from OwnerAddress
alter table NashvilleHousing
add OwnerSplitAddress Nvarchar(255);

Update NashvilleHousing
set OwnerSplitAddress = PARSENAME(Replace(OwnerAddress, ',', '.'), 3)

alter table NashvilleHousing
add OwnerSplitCity Nvarchar(255);

Update NashvilleHousing
set OwnerSplitCity = PARSENAME(Replace(OwnerAddress, ',', '.'), 2)

alter table NashvilleHousing
add OwnerSplitState Nvarchar(255);

Update NashvilleHousing
set OwnerSplitState = PARSENAME(Replace(OwnerAddress, ',', '.'), 1)

Select *
From PortfolioProject.dbo.NashvilleHousing

------------------------------------------------------------------------------------------------------------------------------------

-- Change Y to Yes and N to No in SoldAsVacant column
Select Distinct(SoldAsVacant), count(SoldAsVacant)
From PortfolioProject.dbo.NashvilleHousing
group by SoldAsVacant
order by SoldAsVacant

Select SoldAsVacant
, case when SoldAsVacant = 'Y' then 'Yes'
		when SoldAsVacant = 'N' then 'No'
		else SoldAsVacant
		end
From PortfolioProject.dbo.NashvilleHousing

update NashvilleHousing
set SoldAsVacant = case when SoldAsVacant = 'Y' then 'Yes'
		when SoldAsVacant = 'N' then 'No'
		else SoldAsVacant
		end

------------------------------------------------------------------------------------------------------------------------------------

-- Remove duplicates
with RowNumCTE as(
select *, 
	ROW_NUMBER() over (
	partition by ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 order by
					UniqueID
					) row_num

From PortfolioProject.dbo.NashvilleHousing
)
Delete --delete duplicates
from RowNumCTE
where row_num > 1

------------------------------------------------------------------------------------------------------------------------------------

--Delete unused columns

select *
From PortfolioProject.dbo.NashvilleHousing

alter table PortfolioProject.dbo.NashvilleHousing
drop column OwnerAddress, TaxDistrict, PropertyAddress



