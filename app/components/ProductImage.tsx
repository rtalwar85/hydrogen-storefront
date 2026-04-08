import type {ProductVariantFragment} from 'storefrontapi.generated';
import {Image} from '@shopify/hydrogen';

export function ProductImage({
  image,
  images,
  title,
}: {
  image: ProductVariantFragment['image'];
  images?: Array<{
    id?: string | null;
    url: string;
    altText?: string | null;
    width?: number | null;
    height?: number | null;
  }> | null;
  title?: string;
}) {
  const galleryImages =
    images?.filter((galleryImage) => galleryImage?.url) ?? [];
  const featuredImage = image
    ? [
        image,
        ...galleryImages.filter((galleryImage) => galleryImage.id !== image.id),
      ]
    : galleryImages;

  if (!featuredImage.length) {
    return <div className="product-image" />;
  }

  return (
    <div className="product-image">
      <div className="product-gallery">
        {featuredImage.map((galleryImage, index) => (
          <div className="product-gallery-item" key={galleryImage.id ?? index}>
            <Image
              alt={galleryImage.altText || title || 'Product Image'}
              aspectRatio="3/4"
              data={galleryImage}
              sizes="(min-width: 64em) 42vw, (min-width: 45em) 50vw, 100vw"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
