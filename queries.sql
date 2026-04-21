-- Total Revenue
SELECT SUM(Quantity * UnitPrice) AS Total_Revenue FROM ecommerce;

-- Total Orders
SELECT COUNT(DISTINCT InvoiceNo) AS Total_Orders FROM ecommerce;

-- Top Countries
SELECT Country, SUM(Quantity * UnitPrice) AS Revenue
FROM ecommerce
GROUP BY Country
ORDER BY Revenue DESC
LIMIT 10;
